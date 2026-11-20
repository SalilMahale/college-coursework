#include <stdio.h>

int main(){
    char buff_arr[10];
    int flag = 450;
    printf("\nvalue of flag before (originally set): %d",flag);

    printf("\nenter buffer array within size 10: \n");
    scanf("%s", buff_arr);

    printf("entered array: %s\n", buff_arr);

    printf("value of flag after overflowing: %d\n", flag);
    return 0;
}