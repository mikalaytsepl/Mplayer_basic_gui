#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdlib.h>

enum controls{
    BIG_REW_BW,
    SMALL_REW_BW,
    PLAY_PAUSE,
    SMALL_REW_FW,
    BIG_REW_FW
};

int main(){
    printf("starting the c program ");
    int fd; 
    char *path_to_fifo_file = "/tmp/fifo_for_mplayer";

    unlink(path_to_fifo_file);
    mkfifo(path_to_fifo_file, 0666);

    char *buff = (char*)malloc(11 * sizeof(char));
    
    fd = open(path_to_fifo_file, O_WRONLY); // opening a file descriptor into fifo file with write only permissions
    while(true){

        fgets(buff,11,stdin); // writing user input
        buff[strcspn(buff, "\n")] = '\0';
        int command_code = atoi(buff);

        switch (command_code)
        {
        case BIG_REW_BW:
            write(fd,"seek -60\n",strlen("seek -60\n"));
            break;

        case SMALL_REW_BW:
            write(fd,"seek -10\n",strlen("seek -10\n"));
            break;
        
        case PLAY_PAUSE:
            write(fd,"pause\n",strlen("pause\n"));
            break;
        case SMALL_REW_FW:
            write(fd,"seek 10\n",strlen("seek 10\n"));
            break;

        case BIG_REW_FW:
            write(fd,"seek 60\n",strlen("seek 60\n"));
            break;

         default:
            printf("Invalid command: %s\n", buff);
            break;
        }
        
    }

    free(buff);
    buff = NULL;

    close(fd);
    return 0;
}