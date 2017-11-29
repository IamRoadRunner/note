#include<stdio.h>
#include<stdlib.h>
#include<time.h>

#define random(NumValues)\
	((int)(((double)(rand())*(NumValues))/(RAND_MAX+1.0)))
#define iterations 6
#define test
#define testf
#define repeatable

int sum(int, int);
int product(int, int);
int difference(int, int);

int main(void)
{
	int funsel = 0, a = 10,b = 5,result = 0;
	int (*pfun[])(int, int) = {sum, product, difference};
#if defined repeatable
	srand(1);
#else
	srand((unsigned int)time(NULL));
#endif
int element_count = sizeof(pfun)/sizeof(pfun[0]);
for(int i = 0; i < iterations; i++)
{
	funsel = random(element_count);
	if(funsel>element_count-1)
	{
		printf("\n index=%d",funsel);
		exit(1);
	}
#if defined test
	printf("\n index=%d",funsel);
#endif
	result = pfun[funsel](a,b);
	printf("\nresult = %d",result);
}
return 0;
}

int sum (int x, int y)
{
#if defined testf
	printf("\nsum %d and %d",x, y);
#endif
		return x + y;
}

int product(int x, int y)
{
#if defined testf
	printf("\nproduct%d and %d",x, y);
#endif
		return x * y;
}

int difference(int x, int y)
{
#if defined testf
	printf("\ndifference %d and %d",x, y);
#endif
		return x - y;
}
