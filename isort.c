#include <stdlib.h>
#include <stdio.h>

typedef struct link
{
    int value;
    struct link *next;
} MyLink;

MyLink *iSort(MyLink *head, int value)
{
    MyLink *current = head;
    MyLink *tail = head;
    if (current == NULL)
    {
        printf("current is NULL\n");    
        MyLink *new;
        new = (MyLink *)malloc(sizeof(MyLink));
        new->value = value;
        new->next = NULL;
        return new;
    }
    else 
    {
        printf("in else\n");    
        MyLink *new;
        while ((current->value < value) && (current->next != NULL))
        {
            current = current->next;
        }
        printf("while loop - current->value:  %d\n", current->value);
        new = (MyLink *)malloc(sizeof(MyLink));
        if (current->value < value)
        {
            new->value = value;
            new->next = current->next;
        }
        else
        {
            new->value = current->value;
            current->value = value;
            new->next = current->next;
        }
        current->next = new;
    }
    return head;
}

int main()
{
    MyLink *list, *current;
/*
    list = (MyLink *)malloc(sizeof(MyLink));
    list->value = 5;
    list->next = NULL;
    list = iSort(list, 13);
    list = iSort(list, 1);
    list = iSort(list, -1);
*/
    list = iSort(list, 55);
    current = list;
    while (current)
    {
        printf("current->value:  %d\n", current->value);
        current = current->next;
    } 

    return 0;
}
