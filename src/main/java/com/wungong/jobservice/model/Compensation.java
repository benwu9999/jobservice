package com.wungong.jobservice.model;

import lombok.Data;

@Data
public class Compensation {
	
	private final Double amount;
	
	private final Duration duration;
	
	public Compensation(Double amount, Duration duration) {
		super();
		this.amount = amount;
		this.duration = duration;
	}

	public Double getAmount() {
		return amount;
	}

	public Duration getDuration() {
		return duration;
	}

}
