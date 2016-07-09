package com.wungong.jobservice.model;

import com.datastax.driver.mapping.annotations.UDT;

@UDT(keyspace = "jobservice", name = "duty")
public class Duty {
	
	private String description;

	public Duty(String description) {
		this.description = description;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

}
