from typing import Sequence

def sort_objects_by_parent(
    objects: Sequence,
    related_manager_objects: Sequence
):
    ordering = {
        obj.id: index 
        for index, obj in enumerate(related_manager_objects)
    }
    sorted_objects = sorted(
        objects,
        key=lambda obj: ordering.get(obj.id, float('inf'))
    )
    
    return sorted_objects