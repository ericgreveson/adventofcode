from aoc.challenge_base import ChallengeBase

import numpy as np

class Claim:
    """
    Claim rectangle class
    """
    def __init__(self, uid, x, y, w, h):
        """
        Constructor
        """
        self.uid = uid
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def right(self):
        """
        Get right edge
        """
        return self.x + self.w

    def bottom(self):
        """
        Get bottom edge
        """
        return self.y + self.h

class Challenge(ChallengeBase):
    """
    Day 3 challenges
    """
    def parse_claims(self):
        self.claims = []
        for line in self.lines:
            uid, box = line.split("@")
            pos, size = box.strip().split(":")
            x, y = pos.strip().split(",")
            w, h = size.strip().split("x")
            self.claims.append(Claim(uid.strip(), int(x), int(y), int(w), int(h)))

    def challenge1(self):
        """
        Day 3 challenge 1
        """
        # Load up claim rectangles
        self.parse_claims()

        # Figure out total cloth size
        cloth_w, cloth_h = 0, 0
        for claim in self.claims:
            cloth_w = max(cloth_w, claim.right())
            cloth_h = max(cloth_h, claim.bottom())

        # Allocate cloth matrix and count claims per square
        self.cloth = np.zeros((cloth_h, cloth_w), dtype=np.uint16)
        for claim in self.claims:
            self.cloth[claim.y:claim.bottom(), claim.x:claim.right()] += 1

        # Count squares with claim overlaps
        overlapping_claim_squares = (self.cloth >= 2).sum()
        print(f"Overlapping claim square inches: {overlapping_claim_squares}")

    def challenge2(self):
        """
        Day 3 challenge 2
        """
        # We already have the cloth from the previous challenge
        # Now we just have to go through all claims and check all cloth elements are 1 under each one
        found_uid = None
        for claim in self.claims:
            total_count = self.cloth[claim.y:claim.bottom(), claim.x:claim.right()].sum()
            if total_count == claim.w * claim.h:
                found_uid = claim.uid
                break
        
        print(f"Non-overlapping claim: {found_uid}")
