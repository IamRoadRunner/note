#include<time.h>
#include<stdio.h>
int main(void)
{
	clock_t start, end;
	double cpu_time;
	start = clock();
	end = clock();
	cpu_time = (double)(end-start)/CLOCKS_PER_SEC;
	printf("\n %f",cpu_time);
	return 0;
}
