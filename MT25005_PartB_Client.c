#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>
#include <sys/time.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <msg_size> <duration_sec>\n", argv[0]);
        return 1;
    }

    int msg_size = atoi(argv[1]);
    int duration = atoi(argv[2]);

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr = { .sin_family = AF_INET, .sin_port = htons(8080) };
    inet_pton(AF_INET, "10.0.0.1", &serv_addr.sin_addr);

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connect failed");
        return 1;
    }

    char *buffer = malloc(msg_size);
    long total_bytes = 0;
    struct timeval start, end;
    
    printf("Connected. Running test...\n");
    gettimeofday(&start, NULL);
    time_t end_test = time(NULL) + duration;

    while (time(NULL) < end_test) {
        int bytes = recv(sock, buffer, msg_size, 0);
        if (bytes <= 0) break;
        
        // Check if server sent a rejection message
        if (strncmp(buffer, "REJECTED", 8) == 0) {
            printf("%s", buffer);
            goto end_prog;
        }
        total_bytes += bytes;
    }

    gettimeofday(&end, NULL);

    // --- Part B Calculations ---
    double sec = (end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) / 1e6;
    double gbps = (total_bytes * 8.0) / (sec * 1e9);
    double latency = (sec * 1e6) / (total_bytes / msg_size);

    printf("\n--- Metrics ---\n");
    printf("Throughput: %.4f Gbps\n", gbps);
    printf("Latency:    %.2f us/msg\n", latency);
    printf("Total Data: %.2f MB\n", (double)total_bytes / (1024*1024));

end_prog:
    free(buffer);
    close(sock);
    return 0;
}