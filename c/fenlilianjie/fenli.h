#ifndef _HashSep_H
struct listnode;
typedef struct listnode *position;
struct hashtbl;
typedef struct hashtbl *hashtable;
typedef unsigned int Index;

hashtable Initializetable(int tablesize);
void Destroytable(hashtable h);
position Find(int key, hashtable h);
void Insert(int key,hashtable h);
int Retrieve(position p);
Index Hash(int key,int tablesize);
int NextPrime(int x,int tablesize);

#endif
#define mintablesize 10
struct listnode
{
	int element;
	position next;
/*链表*/
};

typedef position list;
struct hashtbl
{
	int tablesize;
	list *thelists;
/*散列表*/
};
