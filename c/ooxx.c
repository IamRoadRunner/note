#include <stdio.h>
int main(void)
{  
	int player = 0;
	int winner = 0;
	int choice = 0;
	int row = 0;
	int column = 0;
	int line = 0;   
 
	char board[3][3 ] = {
		{'1','2','3'},
		{'4','5','6'},
		{'7','8','9'}
	};
	for(int i = 0; i < 9 && winner == 0; i++)
	{
		printf("\n\n");
		printf("%c |%c |%c\n",board[0][0],board[0][1],board[0][2]);
		printf("---+---+---\n");
		printf("%c |%c |%c\n",board[1][0],board[1][1],board[1][2]);
		printf("---+---+---\n");
		printf("%c |%c |%c\n",board[2][0],board[2][1],board[2][2]);
		player = i%2 + 1;
		do
		{
			printf("\n 玩家%d ,输入位置数字：", player);
			scanf("%d",&choice);
			row = --choice/3;
			column = choice%3;
		}while(choice < 0 || choice > 9 || board[row][column]>'9');
		board[row][column] = (player==1)? 'X':'O';
		if (board[0][0] == board[1][1] && board[0][0] == board[2][2] ||
		(board[0][2] == board[1][1] && board[0][2] == board[2][0]))
			winner = player;
		else
			for (line =0; line <=2; line ++)
				if (board[line][0] == board[line][1] && board[line][0] == board[line][2] ||
				(board[0][line] == board[1][line] && board[0][line] == board[2][line]))
					winner = player;
	}
		printf("\n\n");
		printf("%c |%c |%c\n",board[0][0],board[0][1],board[0][2]);
		printf("---+---+---\n");
		printf("%c |%c |%c\n",board[1][0],board[1][1],board[1][2]);
		printf("---+---+---\n");
		printf("%c |%c |%c\n",board[2][0],board[2][1],board[2][2]);
		if (winner == 0)
			printf("\n it is a draw\n");
		else
			printf("\n player %d is winner", winner);
	return 0;
}
