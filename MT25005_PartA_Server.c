#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>

struct Message { char *fields[8]; };
int mode = 1; 
int test_duration = 0;

void *handle_client(void *socket_desc) {
    int sock = *(int*)socket_desc;
    int total_msg_size = 4096; 
    int field_size = total_msg_size / 8;
    char client_req[1024]; 
    long total_received_from_client = 0;
    
    struct Message msg;
    for (int i = 0; i < 8; i++) {
        msg.fields[i] = malloc(field_size);
        memset(msg.fields[i], 'A' + i, field_size);
    }

    time_t start_time = time(NULL);
    while (time(NULL) - start_time < test_duration) {
        int req_bytes = recv(sock, client_req, sizeof(client_req), 0);
        if (req_bytes <= 0) break;
        
        total_received_from_client += req_bytes;

        if (mode == 1) {
            for (int i = 0; i < 8; i++) send(sock, msg.fields[i], field_size, 0);
        } else {
            struct msghdr out_msg = {0};
            struct iovec iov[8];
            for (int i = 0; i < 8; i++) {
                iov[i].iov_base = msg.fields[i];
                iov[i].iov_len = field_size;
            }
            out_msg.msg_iov = iov;
            out_msg.msg_iovlen = 8;
            sendmsg(sock, &out_msg, 0);
        }
    }

    printf("\n--- Connection Ended ---\n");
    printf("Total data received from the client: %ld bytes\n", total_received_from_client);
    printf("Server cleanup complete.\n");

    for (int i = 0; i < 8; i++) free(msg.fields[i]);
    close(sock);
    free(socket_desc);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <mode: 1, 2, or 3> <duration_sec>\n", argv[0]);
        return 1;
    }
    mode = atoi(argv[1]);
    test_duration = atoi(argv[2]);

    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    
    // Help prevent "Address already in use"
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(9000); // Updated Port

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    listen(server_fd, 3);
    printf("Server running in Mode %d on Port 9000. Waiting for client...\n", mode);

    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))) {
        printf("Get's connected with the client!\n");
        pthread_t thread_id;
        int *new_sock = malloc(sizeof(int));
        *new_sock = new_socket;
        pthread_create(&thread_id, NULL, handle_client, (void*)new_sock);
        pthread_join(thread_id, NULL);
    }

    close(server_fd);
    return 0;
}