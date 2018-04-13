package com.wungong.jobservice.model;

import com.datastax.driver.mapping.annotations.UDT;

@UDT(keyspace = "jobservice", name = "compensation")
public class Compensation {
	
	private Double amount;
	
	private Duration duration;
	
	public Compensation(Double amount, Duration duration) {
		super();
		this.amount = amount;
		this.duration = duration;
	}

	public void setAmount(Double amount) {
		this.amount = amount;
	}

	public void setDuration(Duration duration) {
		this.duration = duration;
	}

	public Double getAmount() {
		return amount;
	}

	public Duration getDuration() {
		return duration;
	}

}
