#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

// Requirement: Message structure with 8 dynamically allocated string fields
struct Message {
    char *fields[8];
};

// Global config (for the sake of this example)
int mode = 1; // 1 = A1 (Two-Copy), 2 = A2 (One-Copy), 3 = A3 (Zero-Copy)

void *handle_client(void *socket_desc) {
    int sock = *(int*)socket_desc;
    int total_msg_size = 4096; // This should match client's expected size
    int field_size = total_msg_size / 8;
    
    // 1. Requirement: Heap-allocate 8 buffers
    struct Message msg;
    for (int i = 0; i < 8; i++) {
        msg.fields[i] = malloc(field_size);
        memset(msg.fields[i], 'A' + i, field_size); // Fill with dummy data
    }

    // A3 Requirement: Enable Zero-Copy at the socket level
    if (mode == 3) {
        int one = 1;
        if (setsockopt(sock, SOL_SOCKET, 60, &one, sizeof(one)) < 0) { // 60 is SO_ZEROCOPY on most Linux
            perror("setsockopt zero-copy failed");
        }
    }

    printf("Thread started. Sending data in Mode %d...\n", mode);

    while (1) {
        if (mode == 1) {
            // A1: Two-Copy using standard send()
            for (int i = 0; i < 8; i++) {
                if (send(sock, msg.fields[i], field_size, 0) <= 0) goto cleanup;
            }
        } 
        else if (mode == 2 || mode == 3) {
            // A2 & A3: Using sendmsg() with iovec (Scatter-Gather)
            struct msghdr out_msg = {0};
            struct iovec iov[8];
            for (int i = 0; i < 8; i++) {
                iov[i].iov_base = msg.fields[i];
                iov[i].iov_len = field_size;
            }
            out_msg.msg_iov = iov;
            out_msg.msg_iovlen = 8;

            int flags = (mode == 3) ? 0x4000000 : 0; // 0x4000000 is MSG_ZEROCOPY
            if (sendmsg(sock, &out_msg, flags) <= 0) goto cleanup;
        }
    }

cleanup:
    for (int i = 0; i < 8; i++) free(msg.fields[i]);
    close(sock);
    free(socket_desc);
    printf("Client disconnected.\n");
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <mode: 1, 2, or 3>\n", argv[0]);
        return 1;
    }
    mode = atoi(argv[1]);

    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8080);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 2);

    printf("Server running in Mode %d. Listening on port 8080...\n", mode);

    while ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))) {
        pthread_t thread_id;
        int *new_sock = malloc(sizeof(int));
        *new_sock = new_socket;
        pthread_create(&thread_id, NULL, handle_client, (void*)new_sock);
        pthread_detach(thread_id);
    }
    return 0;
}