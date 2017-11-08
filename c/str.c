#include <stdio.h>
#include <ctype.h>

int main(void)
{
	char buffer[20];
	int i = 0;
	int letters = 0;
	int digits = 0;
	printf("enter your string:");
	fgets(buffer,sizeof(buffer), stdin);
	while(buffer[i] != '\0')
	{
		letters += isalpha(buffer[i]) != 0;
		digits +=isdigit(buffer[i++]) != 0;
	}
	printf("%d letter,%d digit",letters,digits);
	return 0;
}
