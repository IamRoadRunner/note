#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define NUM_P 100
const size_t BUFFER_LEN = 128;

int main(void)
{
	char buffer[BUFFER_LEN];
	char *pS[NUM_P] = {NULL};
	char *pbuffer = buffer;
	int i = 0;
	printf("\nyou can enter up to %d messages each up to %lu characters",NUM_P,BUFFER_LEN-1);
	for (i = 0; i<NUM_P;i++)
	{
		pbuffer = buffer;
		printf("\nenter %s message,or pass enter to end\n",i>0? "another":"a");
		while((pbuffer - buffer < BUFFER_LEN-1) && 
				((*pbuffer++ = getchar())!='\n'));
		if ((pbuffer - buffer) < 2)
			break;
		if ((pbuffer -  buffer) == BUFFER_LEN && *(pbuffer-1)!='\n')
		{
			printf("string too long - maximum %d characters allowed.",(int)BUFFER_LEN);
			i--;
			continue;
		}
		*(pbuffer - 1) = '\0';
		pS[i] = (char*)malloc(pbuffer-buffer);
		if (pS[i] == NULL)
		{
			printf("\nout of memory - ending program.");
			return 1;
		}
		strcpy(pS[i], buffer);
	}
	printf("\nin reverse order, the strings you entered are:\n");
	while(--i >= 0)
	{
		printf("\n%s",pS[i]);
		free(pS[i]);
		pS[i] = NULL;
	}
	return 0;
}
