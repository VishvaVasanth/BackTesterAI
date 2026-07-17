package com.backtester.backtester.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "strategies")
@Data // Lombok annotation that generates getters, setters, and toString automatically
public class TradingStrategy {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(columnDefinition = "TEXT", nullable = false)
    private String plainEnglishRules;

    private String ticker;
    private LocalDate startDate;
    private LocalDate endDate;

    // Performance Metrics from the Python AI Engine
    private Double totalReturn;
    private Double sharpeRatio;
    private Double maxDrawdown;

    // Storing the time-series equity curve as a JSON string for frontend charts
    @Column(columnDefinition = "TEXT")
    private String equityCurveJson;

    private LocalDateTime createdAt = LocalDateTime.now();
}