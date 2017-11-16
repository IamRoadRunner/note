#include<stdio.h>
#include<stdlib.h>
#include<stdbool.h>
#include<string.h>
#define NUM_P 2

char *str_in(void);
void str_sort( char *[], int);
void swap(char **p1, char **p2);
void str_out(char *[], int);

const size_t BUFFER_LEN = 256;

int main(void)
{
	char *pS[NUM_P];
	int count = 0;
	printf("\nenter lines,pressing enter at the end of each line\n");
	for(count = 0; count < NUM_P; count++)
	if((pS[count] = str_in()) == NULL)
		break;
	str_sort(pS, count);
	str_out(pS, count);
	return 0;
}
char *str_in(void)
{
	char buffer[BUFFER_LEN];
	char *pString = NULL;
	if(fgets(buffer,sizeof(buffer),stdin) == NULL)
	{
		printf("\nerror reading string.\n");
		exit(1);
	}
	if(buffer[0] == '\0')
		return NULL;
	pString = (char*)malloc(strlen(buffer) + 1);
	if(pString == NULL)
	{
		printf("\n out of memory.");
		exit(1);
	}
	return strcpy(pString,buffer);
}
void str_sort(char *p[], int n)
{
	char *pTemp = NULL;
	bool sorted = false;
	while(!sorted)

	{
		sorted = true;
		for (int i=0; i<n-1;i++)
			if (strcmp(p[i],p[i+1])>0)
			{
				sorted = false;
				swap(&p[i], &p[i+1]);
			}
	}
}
void swap(char **p1,char **p2)
{
	char *pt = *p1;
		*p1 = *p2;
		*p2 = pt;
}
void str_out(char *p[],int n)
{
	printf("\n your input sorted in order is :");
	for (int i=0;i < n; i++)
	{
		printf("%s", *p);
		free(*p);
		*p++ = NULL;
	}
	return;
}


