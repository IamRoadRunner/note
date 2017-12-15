#include<stdio.h>
int sushu(int x ,int y)
{
	if (x<10)
	{
		if (y%x==0)
			return sushu(x,++y);
		else
			return sushu(++x,y);
	}
	else
		return y;
}

int main(void)
{
	int a,b;
	printf("enter number :\n");
	scanf("%d,%d",&a,&b);
	return sushu(a,b);
}
