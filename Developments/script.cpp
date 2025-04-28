#include <iostream>
#include <vector>
#include <regex>
#include <string>
#include <optional>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>



int main(int argc, char** argv) {
    int fd[2];
    if (pipe(fd) == -1) {
        std::cerr << "Pipe failed" << std::endl;
        return 1;
    }
    pid_t pid = fork();
    if (pid == -1) {
        std::cerr << "Fork failed" << std::endl;
        return 1;
    } else if (pid == 0) {
        // Child process
        close(fd[0]); // Close read end of pipe
        dup2(fd[1], STDOUT_FILENO); // Redirect stdout to pipe
        dup2(fd[1], STDERR_FILENO); // Redirect stderr to pipe
        close(fd[1]); // Close write end of pipe
        // Execute the command
        char* args[] = { "/bin/bash", "-c", "echo 'Hello, World!'; echo 'Error!' >&2; exit 1;", nullptr };
        execv(args[0], args);
        std::cerr << "Exec failed" << std::endl;

        return 1;
    } else {
        // Parent process
        close(fd[1]); // Close write end of pipe
        wait(NULL); // Wait for child process to finish

    }


    return 0;
}