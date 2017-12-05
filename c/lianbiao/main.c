#include <stdio.h>
#include<stdlib.h>
#include "lianbiao.h"

int main()
{

    return 0;
}

int IsEmpty(List L)
{
    return L->Next == NULL;
}

int IsLast(Position P, List L)
{
    return P->Next == NULL;
}

Position Find(ElementType X, List L)
{
    Position P;
    P = L->Next;
    while(P!=NUll && p->Element!=X)
        P = P->Next;
    return P;
}

void Delete(ElementType X, List L)
{
    Position P, TmpCell;
    P = FindPrevioud(X, L);
    if(!IsLast(P, L))
    {
        TmpCell = P->Next;
        P->Next = TmpCell->Next;
        free(TmpCell);
    }
}

Position FindPrevioud(ElementType X, List L)
{
    Position P;
    P = L;
    whild(P->Next != NULL && P->Next->Element != X)
            P = P->Next;
    return P;
}

void Insert(ElementType X, List L, Position P)
{
    Position TmpCell;
    TmpCell = malloc(sizeof(struct Node));
    if(TmpCell == NULL)
        FatalError("out of space!");
    TmpCell->Element = X;
    TmpCell-> = P->Next;
    P->Next = TmpCell;
}



























