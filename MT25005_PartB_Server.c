#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdatomic.h>

struct Message {
    char *fields[8];
};

atomic_int active_clients = 0; 
#define MAX_CLIENTS 4
int transmission_mode = 1; 

void *handle_client(void *socket_desc) {
    int sock = *(int*)socket_desc;
    int total_msg_size = 4096; // Adjust based on experiment
    int field_size = total_msg_size / 8;
    
    struct Message msg;
    for (int i = 0; i < 8; i++) {
        msg.fields[i] = malloc(field_size);
        memset(msg.fields[i], 'A' + i, field_size); 
    }

    if (transmission_mode == 3) {
        int one = 1;
        setsockopt(sock, SOL_SOCKET, 60, &one, sizeof(one)); // SO_ZEROCOPY
    }

    while (1) {
        if (transmission_mode == 1) {
            for (int i = 0; i < 8; i++) {
                if (send(sock, msg.fields[i], field_size, 0) <= 0) goto cleanup;
            }
        } 
        else {
            struct msghdr out_msg = {0};
            struct iovec iov[8];
            for (int i = 0; i < 8; i++) {
                iov[i].iov_base = msg.fields[i];
                iov[i].iov_len = field_size;
            }
            out_msg.msg_iov = iov;
            out_msg.msg_iovlen = 8;
            int flags = (transmission_mode == 3) ? 0x4000000 : 0; 
            if (sendmsg(sock, &out_msg, flags) <= 0) goto cleanup;
        }
    }

cleanup:
    for (int i = 0; i < 8; i++) free(msg.fields[i]);
    close(sock);
    free(socket_desc);
    active_clients--; 
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <mode: 1, 2, 3>\n", argv[0]);
        return 1;
    }
    transmission_mode = atoi(argv[1]);

    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY; 
    address.sin_port = htons(8080);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 10);

    printf("Server Mode %d. Max: %d. Waiting...\n", transmission_mode, MAX_CLIENTS);

    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&opt);
        
        if (active_clients >= MAX_CLIENTS) {
            char *reject = "REJECTED: Server Full\n";
            send(new_socket, reject, strlen(reject), 0);
            close(new_socket);
            continue;
        }

        active_clients++;
        pthread_t tid;
        int *ns = malloc(sizeof(int));
        *ns = new_socket;
        pthread_create(&tid, NULL, handle_client, ns);
        pthread_detach(tid);
    }
    return 0;
}