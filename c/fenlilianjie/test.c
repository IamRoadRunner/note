#include<stdio.h>
int NextPrime(int tablesize)
{
	int i=2;
	while(tablesize%i!=0)
	{
		if (i<9)
			i++;
		else if (i=9)
				return tablesize;
	}
}
int main(void)
{
	int a=0;
	printf("enter int num，>10");
	scanf("%d",&a);
	while(NextPrime(a)!=a)
	{
		++a;
	}
	return NextPrime(a);
}
