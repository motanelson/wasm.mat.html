#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <time.h>
#include <math.h>

#include <emscripten.h>
int count=0;
int play=1;
int x=0;
int y=0;
void Start_game(){
     printf ( "start game\n" );
}
void End_game(){
     printf ( "end game\n" );
     play=0;
}
void Play_Game(){
    x++;
    y++;
    printf("x:%d,y:%d\n",x,y);
}
void kernel_main(){
     if (play){
         if(count==0)Start_game();
         if(count==20)End_game();
         if(count>1 && count<19)Play_Game();
         count++;
     }
}

int main() {
    emscripten_set_main_loop(kernel_main,1,0);
    return 0;
}