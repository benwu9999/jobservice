package com.wungong.jobservice.model;

import com.datastax.driver.mapping.annotations.UDT;

@UDT(keyspace = "jobservice", name = "benefit")
public class Benefit {
	
	private String description;

	public Benefit(String description) {
		this.description = description;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

}
