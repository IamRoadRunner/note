#include<stdio.h>

int sum(int, int);
int product(int, int);
int difference(int, int);
int any_function(int(*pfun)(int, int),int x, int y);

int main(void)
{
	int a = 10;
	int b = 5;
	int result = 0;
	int (*pfun)(int,int) = sum;
	result = any_function(pfun, a, b);
	printf("\nresult = %d",result);
	result = any_function(product, a, b);
	printf("\nresult = %d",result);
	result = any_function(difference, a, b);
	printf("\nresult = %d",result);
return 0;
}
int any_function(int(*pfun)(int, int), int x, int y)
{
	return pfun(x,y);
}
int sum(int x,int y)
{
	return x+y;
}
int product(int x,int y)
{
	return x*y;
}
int difference(int x,int y)
{
	return x-y;
}
