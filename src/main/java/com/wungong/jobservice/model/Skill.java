package com.wungong.jobservice.model;

import lombok.Data;

@Data
public class Skill {
	
	private final String description;

	public Skill(String description) {
		this.description = description;
	}

	public String getDescription() {
		return description;
	}

}
