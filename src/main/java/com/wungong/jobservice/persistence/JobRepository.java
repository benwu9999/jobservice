package com.wungong.jobservice.persistence;

import java.util.UUID;

import com.wungong.jobservice.model.Job;

public interface JobRepository {

	UUID jobId();
	
	Job jobOfId(UUID jobId);

	Boolean remove(Job jobToDelete);

	void add(Job convertToJob);

}
