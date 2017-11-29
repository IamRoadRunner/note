#include<stdio.h>
#include<string.h>
#define max(x, y) x > y ? x : y
#define str 1 
/*#define join(x,y) x##y*/

int main(void)
{
	int a = 0;
	printf("\nenter a int number:");
	scanf("%d",&a);
	printf("%d\n",max(a,5));
	printf("%d",str);
/*	strlen(join(var,123));*/
	printf("\nat %s on %s",__TIME__,__DATE__);
	return 0;
}
