package com.example.voting.controller;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.voting.model.Candidate;
import com.example.voting.model.Vote;
import com.example.voting.repository.CandidateRepository;
import com.example.voting.repository.UserRepository;
import com.example.voting.repository.VoteRepository;

@RestController
@RequestMapping("/api/admin")
public class AdminController {
    @Autowired private VoteRepository voteRepo;
    @Autowired private CandidateRepository candidateRepo;
    @Autowired private UserRepository userRepo;    @GetMapping("/votes")
    public List<Vote> getAllVotes() {
        return voteRepo.findAll();
    }

    @DeleteMapping("/votes/reset")
    public ResponseEntity<?> resetVotes() {
        voteRepo.deleteAll();
        // Reset all user voting status
        userRepo.findAll().forEach(user -> {
            user.setHasVoted(false);
            userRepo.save(user);
        });
        // Reset all candidate vote counts
        candidateRepo.findAll().forEach(candidate -> {
            candidate.setVotesCount(0);
            candidateRepo.save(candidate);
        });        return ResponseEntity.ok().body("All votes have been reset");
    }

    @PostMapping("/candidates")
    public ResponseEntity<?> addCandidate(@RequestBody Map<String, String> body) {
        String name = body.get("name");
        if (name == null || name.trim().isEmpty()) {
            return ResponseEntity.badRequest().body("Candidate name is required");
        }
        Candidate candidate = new Candidate();
        candidate.setName(name.trim());
        candidate.setVotesCount(0);
        return ResponseEntity.ok(candidateRepo.save(candidate));
    }

    @DeleteMapping("/candidates/{id}")
    public ResponseEntity<?> removeCandidate(@PathVariable Long id) {
        candidateRepo.deleteById(id);
        return ResponseEntity.ok().body("Candidate removed");
    }

    @GetMapping("/export/csv")
    public ResponseEntity<String> exportToCSV() {
        StringBuilder csv = new StringBuilder();
        csv.append("Candidate,Votes\n");

        candidateRepo.findAll().forEach(candidate -> {
            csv.append(String.format("%s,%d\n",
                    candidate.getName(),
                    candidate.getVotesCount()));
        });

        return ResponseEntity
                .ok()
                .header("Content-Type", "text/csv")
                .header("Content-Disposition", "attachment; filename=\"voting-results.csv\"")
                .body(csv.toString());
    }
}

