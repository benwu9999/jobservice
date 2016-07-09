package com.wungong.jobservice.model;

import com.datastax.driver.mapping.annotations.UDT;

@UDT(keyspace = "jobservice", name = "skill")
public class Skill {
	
	private String description;

	public Skill(String description) {
		this.description = description;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

}
