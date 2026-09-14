"""
Homework 2: The Playlist Shuffler -- starter.

Complete CircularPlaylist below. See HW2_The_Playlist_Shuffler.md,
Part B, for the full requirements.
"""

from typing import List, Optional


class _SongNode:
    __slots__ = ("name", "next")

    def __init__(self, name: str) -> None:
        self.name = name
        self.next: Optional["_SongNode"] = None


class CircularPlaylist:
    def __init__(self) -> None:
        self._current: Optional[_SongNode] = None  # the "currently playing" node
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def add_song(self, name: str) -> None:
        """Insert `name` at the end of the circle (its next wraps back to the head)."""
        new_node = _SongNode(name)

        # Empty playlist
        if self._current is None:
            new_node.next = new_node
            self._current = new_node
            self._size = 1
            return

        # Find the last node.
        # The head is the node after the last node.
        head = self._current
        last = head

        while last.next is not head:
            last = last.next

        # Insert the new node at the end.
        last.next = new_node
        new_node.next = head

        self._size += 1

    def skip_next(self) -> str:
        """Advance the currently-playing pointer to the next song and return its name."""
        if self._current is None:
            raise IndexError("playlist is empty")

        self._current = self._current.next
        return self._current.name

    def remove_current(self) -> str:
        """
        Remove the currently-playing song, rewire the circle around it,
        advance to the next song, and return the name of the removed song.
        """
        if self._current is None:
            raise IndexError("playlist is empty")

        removed_name = self._current.name

        # Only one song remains.
        if self._size == 1:
            self._current = None
            self._size = 0
            return removed_name

        # Find the node immediately before the current node.
        previous = self._current

        while previous.next is not self._current:
            previous = previous.next

        # Skip over the current node.
        next_node = self._current.next
        previous.next = next_node

        # Advance to the next song.
        self._current = next_node

        self._size -= 1

        return removed_name

    def elimination_shuffle(self, k: int) -> List[str]:
        """
        Repeatedly skip k-1 songs and remove the k-th (the Josephus
        pattern from Part A, Question 3), until one song remains.
        Return the removed songs in removal order, with the survivor
        as the final element of the list.
        """
        if k <= 0:
            raise ValueError("k must be positive")

        removal_order = []

        # Stop when exactly one song remains.
        while self._size > 1:

            # Skip k - 1 songs.
            for _ in range(k - 1):
                self.skip_next()

            # Remove the k-th song.
            removal_order.append(self.remove_current())

        # Add the final survivor.
        if self._current is not None:
            removal_order.append(self._current.name)

        return removal_order