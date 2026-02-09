#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <msg_size_bytes> <duration_sec>\n", argv[0]);
        return 1;
    }

    int msg_size = atoi(argv[1]);
    int duration = atoi(argv[2]);

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(9000); // Matches the new Server port

    // IMPORTANT: Target the IP assigned to ns_server in your script
    if (inet_pton(AF_INET, "10.0.0.1", &serv_addr.sin_addr) <= 0) {
        printf("Invalid address/ Address not supported\n");
        return 1;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection Failed"); 
        return 1;
    }

    printf("Get's connected with the server!\n");

    char *buffer = malloc(msg_size);
    char *request = "REQ_DATA"; 
    long total_bytes = 0;
    long iterations = 0;
    double total_latency = 0;

    struct timespec start_total, end_total, start_iter, end_iter;
    clock_gettime(CLOCK_MONOTONIC, &start_total);

    while (1) {
        clock_gettime(CLOCK_MONOTONIC, &start_iter);
        if (send(sock, request, strlen(request), 0) <= 0) break;

        int received = 0;
        while (received < msg_size) {
            int bytes = recv(sock, buffer + received, msg_size - received, 0);
            if (bytes <= 0) goto end_loop;
            received += bytes;
        }

        clock_gettime(CLOCK_MONOTONIC, &end_iter);
        total_latency += (end_iter.tv_sec - start_iter.tv_sec) + (end_iter.tv_nsec - start_iter.tv_nsec) / 1e9;
        total_bytes += received;
        iterations++;

        clock_gettime(CLOCK_MONOTONIC, &end_total);
        if ((end_total.tv_sec - start_total.tv_sec) >= duration) break;
    }

end_loop:
    printf("\nConnection ended.\n");
    if (iterations > 0) {
        printf("Total Data Received: %ld bytes\n", total_bytes);
    }

    free(buffer);
    close(sock);
    return 0;
}