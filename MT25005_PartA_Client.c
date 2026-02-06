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
    serv_addr.sin_port = htons(8080);
    inet_pton(AF_INET, "10.0.0.1", &serv_addr.sin_addr); // IP inside namespace

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection Failed");
        return 1;
    }

    char *buffer = malloc(msg_size);
    time_t start_time = time(NULL);
    long total_bytes = 0;

    printf("Connected. Receiving for %d seconds...\n", duration);

    while (time(NULL) - start_time < duration) {
        int bytes = recv(sock, buffer, msg_size, 0);
        if (bytes <= 0) break;
        total_bytes += bytes;
    }

    printf("Finished.\nTotal Received: %.2f GB\n", (double)total_bytes / (1024*1024*1024));

    free(buffer);
    close(sock);
    return 0;
}