package com.wungong.jobservice.controller;

import javax.ws.rs.core.Response;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.wungong.jobservice.request.CreateJobRequest;
import com.wungong.jobservice.request.UpdateJobRequest;
import com.wungong.jobservice.response.JobResponse;
import com.wungong.jobservice.response.JobResponseImpl;
import com.wungong.jobservice.service.JobService;

@RestController
@RequestMapping("/job")
public class JobserviceController {
	
	@Autowired
	JobService jobservice;
	
	@RequestMapping(method = RequestMethod.POST, consumes="application/json", produces="application/json")
    public JobResponse createJob(CreateJobRequest request) {
		jobservice.createJob(request);
		return new JobResponseImpl(Response.Status.CREATED);
    }
	
	@RequestMapping(method = RequestMethod.DELETE, params="id", produces="application/json")
	public JobResponse deleteJob(@RequestParam("id") String id) {
		jobservice.deleteJob(id);
		return new JobResponseImpl(Response.Status.OK);
    }
	
	@RequestMapping(method = RequestMethod.PUT, consumes="application/json", produces="application/json")
    public JobResponse updateJob(UpdateJobRequest request) {
		jobservice.updateJob(request);
		return new JobResponseImpl(Response.Status.OK);
    }
	
	@RequestMapping(method = RequestMethod.GET, params="id", produces="application/json")
    public JobResponse getJob(@RequestParam("id") String id) {
		jobservice.getJob(id);
		return new JobResponseImpl(Response.Status.OK);
    }
}
