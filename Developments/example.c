
#define SHA256_DIGEST_LENGTH 32
#define FLDSIZE_X 80
#define FLDSIZE_Y 24
#define MAX(a,b) ((a) > (b) ? (a) : (b))
#define MIN(a,b) ((a) < (b) ? (a) : (b))
#include <stdio.h>
#include <string.h>



int main() {
    int i, b;
    int x = 0, y = 0;
    int field[FLDSIZE_X][FLDSIZE_Y];
    
    unsigned char dgst_raw[SHA256_DIGEST_LENGTH];
    unsigned char dgst_raw_len = SHA256_DIGEST_LENGTH;

    /* initialize the field */
    for (i = 0; i < FLDSIZE_X; i++)
            for (b = 0; b < FLDSIZE_Y; b++)
                    field[i][b] = 0;

    /* augment the field */


    char* augmentation_string = " .o+=*BOX@%&#/^SE";
    int len = strlen(augmentation_string);
    for (i = 0; i < dgst_raw_len; i++) {
        int input;
        /* each byte conveys four 2-bit move commands */
        input = dgst_raw[i];
        for (b = 0; b < 4; b++) {
            /* evaluate 2 bit, rest is shifted later */
            x += (input & 0x1) ? 1 : -1;
            y += (input & 0x2) ? 1 : -1;

            /* assure we are still in bounds */
            x = MAX(x, 0);
            y = MAX(y, 0);
            x = MIN(x, FLDSIZE_X - 1);
            y = MIN(y, FLDSIZE_Y - 1);

            /* augment the field */
            if (field[x][y] < len - 2)
                field[x][y]++;
            input = input >> 2;
        }
    }
        
    return 0;
}