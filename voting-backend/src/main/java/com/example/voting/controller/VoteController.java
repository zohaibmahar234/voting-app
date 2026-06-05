 package com.example.voting.controller;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.voting.model.Candidate;
import com.example.voting.model.User;
import com.example.voting.model.Vote;
import com.example.voting.repository.CandidateRepository;
import com.example.voting.repository.UserRepository;
import com.example.voting.repository.VoteRepository;
import com.example.voting.service.SseService;

@RestController
@RequestMapping("/api/vote")
public class VoteController {    @Autowired private UserRepository userRepo;
    @Autowired private CandidateRepository candidateRepo;
    @Autowired private VoteRepository voteRepo;
    @Autowired private SseService sseService;

    @PostMapping("/submit")
    @Transactional
    public ResponseEntity<?> submitVote(@RequestBody Map<String, Object> body) {
        Long userId = Long.valueOf(body.get("userId").toString());
        Long candidateId = Long.valueOf(body.get("candidateId").toString());

        User user = userRepo.findById(userId).orElse(null);
        Candidate candidate = candidateRepo.findById(candidateId).orElse(null);
        if (user == null || candidate == null) return ResponseEntity.badRequest().body("Invalid IDs");
        if (user.getHasVoted()) return ResponseEntity.status(403).body("Already voted");

        user.setHasVoted(true);
        candidate.setVotesCount(candidate.getVotesCount() + 1);
        Vote vote = new Vote();
        vote.setUser(user); vote.setCandidate(candidate);

        userRepo.save(user);
        candidateRepo.save(candidate);
        voteRepo.save(vote);
        sseService.broadcastVoteCounts();
        return ResponseEntity.ok("Vote submitted");
    }
}

