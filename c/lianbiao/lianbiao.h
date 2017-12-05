//
// Created by wang on 12/1/17.
//

#ifndef LIANBIAO_LIANBIAO_H
#define LIANBIAO_LIANBIAO_H

#endif //LIANBIAO_LIANBIAO_H
struct Node;
typedef struct Node *PtrToNode;
typedef PtrToNode List;
typedef PtrToNode Position;

List MakeEmpty(List L);


int IsEmpty(List L);
int IsLast(Position P, List L);
Position Find(ElementType X, List L);
void Delete(ElementType X, List L);
Position FindPrevioud(ElementType X, List L);
void Insert(ElementType X, List L, Position P);


void DeleteList(List L);
Position Header(List L);
Position First(List L);
Position Advance(Position P);
ElementType Retrieve(Position P);

struct Node
{
    ElementType Element;
    Position Next;
};