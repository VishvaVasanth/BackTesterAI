package com.backtester.backtester.repository;

import com.backtester.backtester.entity.TradingStrategy;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StrategyRepository extends JpaRepository<TradingStrategy, Long> {
    // Standard CRUD operations (Save, Find, Delete) are handled out-of-the-box by Spring Data JPA
}