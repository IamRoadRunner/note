#ifndef _HashSep_H
struct listnode;
typedef struct listnode *position;
struct hashtbl;
typedef struct hashtbl *hashtable;

hashtable Initializetalbe(int tablesize);
void Destroytable(hashtable h);
position Find(int key, hashtable h);
void Insert(int key,hashtable h);
int Retrieve(position p);
#endif

struct listnode
{
	int element;
	position next;
};

typedef position list;
struct hashtbl
{
	int tablesize;
	list *thelists;
}
