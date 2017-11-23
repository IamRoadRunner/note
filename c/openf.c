#include<stdio.h>
#include<string.h>
#include<stdlib.h>
const int LENGTH = 80;

int main(void)
{
	char mystr[LENGTH];
	int lstr = 0;
	int mychar = 0;
	FILE *pfile = NULL;
	char *filename =  "test.c";
	printf("\nenter string less than 80 characters:\n");
	fgets(mystr,LENGTH, stdin);
	if(!(pfile = fopen(filename,"a")))
	{
		printf("error");
		exit(1);
	}
	lstr = strlen(mystr);
	for (int i = 0;i<lstr;i++)
		fputc(mystr[i],pfile);
	fputs("********\0",pfile);
	fclose(pfile);
	if(!(pfile = fopen(filename, "r")))
	{
		printf("error");
		exit(1);
	}
	while((mychar = fgetc(pfile))!=EOF)
		putchar(mychar);
	putchar('\n');
	fclose(pfile);
/*	remove(filename);*/
/*	if (rename("test.c","test2.c"))
		printf("error");
	else
		printf("ok");*/
/*	remove("test2.c");*/
	return 0;
}

