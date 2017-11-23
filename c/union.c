#include<stdio.h>
int main(void)
{
	union u_example
	{
		float decval;
		int pnum;
		double my_value;
	}u;
	u.my_value = 125.5;
	u.pnum = 10;
	u.decval = 1000.5f;
	printf("\nd = %f;p = %d;m = %lf\n",u.decval,u.pnum,u.my_value);
	printf("\nu = %d,d = %d",(int)sizeof u,(int)sizeof u.decval );
	return 0;
}
