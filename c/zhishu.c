#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(void)
{
	unsigned long *primes = NULL;
	unsigned long trial = 0;
	bool found = false;
	size_t total = 0;
	size_t count = 0;
	printf("how many primes? least 4:");
	scanf("%lu",&total);
	total = total<4U? 4U:total;
	primes = (unsigned long *)malloc(total*sizeof(unsigned long));
	if (primes==NULL)
	{
		printf("\nnot enough memory.");
		return 1;
	}
	*primes = 2UL;
	*(primes+1) = 3UL;
	*(primes+2) = 5UL;
	count = 3U;
	trial = 5U;
	while(count < total)
	{
		trial+=2UL;
		for(size_t i = 1;i<count;i++)
			if(!(found = (trial % *(primes+i))))
				break;
		if(found)
			*(primes+count++) = trial;
	}
	for (size_t i=0;i<total;i++)
	{
		if (!(i%5U))
			printf("\n");
		printf("%3lu",*(primes+i));
	}
	printf("\n");
	return 0;
}
