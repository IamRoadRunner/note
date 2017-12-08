#include<stdio.h>
#include<stdlib.h>
int main(void)
{
	struct horse
	{
		struct date
		{
			int day;
		}bob;
		int age;
		char name[20];
	};
	int count = 0;
	struct horse *phorse[3];
	for (count = 0; count<3; count++)
	{
		phorse[count] = (struct horse*)malloc(sizeof(struct horse));
		printf("enter age:");
		scanf("%d",&phorse[count]->age);
		printf("enter name:");
		scanf("%s", &phorse[count]->name);
		printf("enter day:");
		scanf("%d", &phorse[count]->bob.day);	
	}
	for (int i = 0; i<=count;i++)
	{
		printf("age:%d,name:%s,day:%d\n",phorse[i]->age,phorse[i]->name,phorse[i]->bob.day);
		free(phorse[i]);
	}
	return 0;
}
