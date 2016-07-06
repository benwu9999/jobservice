package com.wungong.jobservice.persistence;

import com.wungong.jobservice.model.Job;
import com.wungong.jobservice.model.JobId;

public interface JobRepository {

	JobId jobId();
	
	Job jobOfId(JobId jobId);

	Boolean remove(Job jobToDelete);

	void add(Job convertToJob);

}
