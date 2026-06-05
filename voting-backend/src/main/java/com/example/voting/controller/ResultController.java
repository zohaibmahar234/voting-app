 package com.example.voting.controller;

import com.example.voting.model.Candidate;
import com.example.voting.repository.CandidateRepository;
import com.example.voting.service.SseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.util.List;

@RestController
@RequestMapping("/api/results")
public class ResultController {
    @Autowired private CandidateRepository candidateRepo;
    @Autowired private SseService sseService;

    @GetMapping
    public List<Candidate> getResults() {
        return candidateRepo.findAll();
    }

    @GetMapping(path = "/stream", produces = "text/event-stream")
    public SseEmitter stream() {
        return sseService.createEmitter();
    }
}

