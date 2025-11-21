from functools import lru_cache
from typing import Dict, Set, List, Iterator, Optional, Tuple

class SetlistSolver:
    """
    Finds and counts valid sequences of teams (setlists) where no two
    adjacent teams share a member (Hamiltonian paths in a compatibility graph).
    """

    def __init__(self, teams_to_members: Dict[str, Set[str]]):
        if not teams_to_members:
            raise ValueError("Input `teams_to_members` cannot be empty.")

        # Light sanitization: strip whitespace around member names
        self.teams_to_members: Dict[str, Set[str]] = {
            team: {str(m).strip() for m in members}
            for team, members in teams_to_members.items()
        }

        self.teams: List[str] = list(self.teams_to_members.keys())
        self.team_count: int = len(self.teams)
        self.team_to_idx: Dict[str, int] = {team: i for i, team in enumerate(self.teams)}
        self.adjacency_masks: List[int] = self._build_compatibility_graph()

    def _build_compatibility_graph(self) -> List[int]:
        """Bitmask adjacency: adj[i] has bit j set iff team i is compatible with j."""
        adj = [0] * self.team_count
        for i, team_i in enumerate(self.teams):
            members_i = self.teams_to_members[team_i]
            mask = 0
            for j, team_j in enumerate(self.teams):
                if i == j:
                    continue
                if self.teams_to_members[team_j].isdisjoint(members_i):
                    mask |= (1 << j)
            adj[i] = mask
        return adj

    # ---------- Generate valid setlists (optional start/end constraints) ----------

    def generate_valid_setlists(
        self,
        limit: Optional[int] = None,
        start_team: Optional[str] = None,
        end_team: Optional[str] = None,
        debug: bool = False,
    ) -> Iterator[List[str]]:
        """
        Backtracking + heuristics. Before yielding, we STRICTLY validate that
        each adjacent pair shares no members (guarding against data issues).
        """
        if start_team and start_team not in self.team_to_idx:
            raise ValueError(f"Start team '{start_team}' not found.")
        if end_team and end_team not in self.team_to_idx:
            raise ValueError(f"End team '{end_team}' not found.")

        # Heuristic: try nodes with fewer neighbors first (tighter first)
        ranked_indices = sorted(
            range(self.team_count),
            key=lambda i: bin(self.adjacency_masks[i]).count("1")
        )
        idx_to_rank = {orig: r for r, orig in enumerate(ranked_indices)}

        # Reindex adjacency + names according to ranking
        adj_r = [0] * self.team_count
        teams_r = [self.teams[i] for i in ranked_indices]
        for i in range(self.team_count):
            original_mask = self.adjacency_masks[i]
            m = 0
            for j in range(self.team_count):
                if (original_mask >> j) & 1:
                    m |= (1 << idx_to_rank[j])
            adj_r[idx_to_rank[i]] = m

        start_node_r = idx_to_rank[self.team_to_idx[start_team]] if start_team else None
        end_node_r   = idx_to_rank[self.team_to_idx[end_team]]   if end_team   else None

        produced = 0
        for path_indices in self._backtrack_with_end(adj_r, start_node_r, end_node_r):
            if limit is not None and produced >= limit:
                return

            # Convert to team names
            seq = [teams_r[i] for i in path_indices]

            # STRICT VALIDATION: verify every adjacent pair has disjoint members
            ok, conflict = self._sequence_is_valid(seq)
            if not ok:
                if debug:
                    a, b, overlap = conflict
                    print(f"[skip invalid] {a} -> {b} shares members: {sorted(overlap)}")
                continue

            yield seq
            produced += 1

    def _backtrack_with_end(
        self,
        adj_r: List[int],
        start_node_r: Optional[int],
        end_node_r: Optional[int],
    ) -> Iterator[List[int]]:
        """
        Enforce fixed end by forbidding `end_node_r` until last slot and
        forcing it at the final step (if reachable).
        """
        n = self.team_count
        path: List[int] = []
        used_mask = 0

        def solve():
            nonlocal used_mask
            L = len(path)
            if L == n:
                if end_node_r is None or path[-1] == end_node_r:
                    yield path.copy()
                return

            if L == 0:
                candidates = [start_node_r] if start_node_r is not None else list(range(n))
            else:
                last = path[-1]
                allowed = adj_r[last] & ~used_mask

                if end_node_r is not None and L < n - 1:
                    allowed &= ~(1 << end_node_r)

                if end_node_r is not None and L == n - 1:
                    if (allowed >> end_node_r) & 1:
                        allowed = (1 << end_node_r)
                    else:
                        return  # cannot reach required end

                candidates = []
                x = allowed
                while x:
                    lsb = x & -x
                    candidates.append(lsb.bit_length() - 1)
                    x ^= lsb

                # heuristic: fewest future options first
                candidates.sort(key=lambda c: bin(adj_r[c] & ~used_mask).count("1"))

            for c in candidates:
                if (used_mask >> c) & 1:
                    continue
                path.append(c)
                used_mask |= (1 << c)
                yield from solve()
                used_mask &= ~(1 << c)
                path.pop()

        yield from solve()

    # ---------- Validation & Debug helpers ----------

    def _sequence_is_valid(self, seq: List[str]) -> Tuple[bool, Optional[Tuple[str, str, Set[str]]]]:
        """Return (True, None) if valid; else (False, (teamA, teamB, overlapping_members))."""
        for a, b in zip(seq, seq[1:]):
            overlap = self.teams_to_members[a] & self.teams_to_members[b]
            if overlap:
                return False, (a, b, overlap)
        return True, None

    def explain_pair(self, team_a: str, team_b: str) -> None:
        """Print the intersection (if any) for a quick manual check."""
        inter = self.teams_to_members[team_a] & self.teams_to_members[team_b]
        if inter:
            print(f"{team_a} and {team_b} share: {sorted(inter)}")
        else:
            print(f"{team_a} and {team_b} are compatible (no shared members).")


# ----------------------- Example Usage -----------------------

if __name__ == "__main__":
    # Example data (replace with your real mapping)
    sample_teams_data = {
        "go": {"meso", "sophia_z", "luke", "leo_z", "justin", "angie", "timothy"},
        "dirty_work": {"hairuo", "aslan", "sabrina", "kaiki"},
        "guilty": {"sophia_z", "weilun", "sohpia_d", "joey", "vivian"},
        "last_festival": {"andy", "roxanne", "sean", "brandon", "irene", "max"},
        "famous": {"leo_s", "kaiki", "hairuo", "elena", "joey"},
        "jellyous": {"kaylee", "michael", "sabrina", "max", "lisa"},
        "bad_villain": {"andy", "meso", "haeun", "eni", "mandy", "hairuo", "vivian"},
        "drip": {"talia", "irene", "irving", "phuong", "yuna"},
        "loco": {"ava", "sua", "adell", "aslan", "elena"},
        "plot_twist": {"leo_s", "andrew_liu", "lisa", "brandon", "sophia_z", "timothy"},
        "nxde": {"angela", "sherla", "eni", "meso", "aslan"},
        "siren": {"talia", "kaiki", "phuong", "chi", "adell", "kaylee", "sean"},
        "hot": {"roxanne", "neha", "sarea", "sua", "ava"},
        "xoxz": {"aslan", "andrew_lee", "talia", "chunzhen", "irene", "sarea"},
        "grabriela": {"vivian", "haeun", "michael", "angela", "sherla"},
        "dope": {"joey", "max", "andrew_lee", "andy", "sophia_d", "kaylee", "leo_s"}
    }

    solver = SetlistSolver(sample_teams_data)

    # Quick sanity check for your specific complaint:
    # Uncomment to see exactly what they share in YOUR data.
    # solver.explain_pair("plot_twist", "famous")

    print(f"Working with {solver.team_count} teams.")

    # Find setlists with fixed start, end, AND MULTIPLE fixed middle teams
    try:
        # --- Define all of your constraints here ---
        start = "go"
        end = "dope"

        # First positional constraint
        target_team_1 = "xoxz"
        target_position_index_1 = 8

        # Second positional constraint
        target_team_2 = "bad_villain"
        target_position_index_2 = 7

        # Third positional constraint
        target_team_3 = "siren"
        target_position_index_3 = 11

        # Fourth positional constraint
        target_team_4 = "drip"
        target_position_index_4 = 14
        # -----------------------------------------
        
        print(
            f"\n--- Finding setlists starting with '{start}', ending with '{end}', "
            f"with '{target_team_1}' in position {target_position_index_1 + 1}, "
            f"'{target_team_2}' in position {target_position_index_2 + 1}, "
            f"'{target_team_3}' in position {target_position_index_3 + 1}, "
            f"and '{target_team_4}' in position {target_position_index_4 + 1} ---"
        )

        found_count = 0
        limit = 10  # Find up to 10 examples

        # Call the generator with the start and end teams locked
        generator = solver.generate_valid_setlists(
            start_team=start,
            end_team=end
        )

        # Loop through the results and apply all positional checks
        for setlist in generator:
            # Check all four positional constraints
            if (
                len(setlist) > target_position_index_1
                and setlist[target_position_index_1] == target_team_1
                and len(setlist) > target_position_index_2
                and setlist[target_position_index_2] == target_team_2
                and len(setlist) > target_position_index_3
                and setlist[target_position_index_3] == target_team_3
                and len(setlist) > target_position_index_4
                and setlist[target_position_index_4] == target_team_4
            ):
                found_count += 1
                print(f"{found_count}: {setlist}")

            if found_count >= limit:
                break

        if found_count == 0:
            print("No valid setlists found that satisfy all specified conditions.")

    except ValueError as e:
        print(f"Error: {e}")