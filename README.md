# Lambda function to delete unused EBS volumes

This code is a simple representation of how a quick cleanup of EBS volumes that are not in use could be done.

It is not necessarily a solution that adapts to any need, there are other governance tools such as [Cloud Custodian](https://cloudcustodian.io/) or [CloudCheckr](https://cloudcheckr.com/) that will allow you to carry out these cleaning tasks in a more dynamic and controlled way.

## How it works

This lambda function is scheduled to be executed every minute. Will look into the EC2 client to retrieve volumes filtered by state: `available`, which means, volumes that are not attached to any instance right now.

Taking into consideration there's is a possibility to create instances and indicates whether the volume should be automatically deleted when the instance is terminated, you may fall into unnecessary costs for EBS volumes that were not deleted in the same time as the EC2 instance was terminated.

In order to avoid this extra cost, this lambda function will ask for volumes with no instances attached and proceed to delete it.

## How to deploy

This is a regular [serverless](https://www.serverless.com/) project, so proceed to [install the CLI](https://www.serverless.com/framework/docs/getting-started) and deploy this project using:

```sh
serverless deploy
```

Take into consideration you need a valid credentials already loaded so serverless can know where to deploy this new stack.

## How to test

### Scenario #1: 

Create an EC2 instance and make sure to set `delete_on_termination` as `false`. Using the console, this is a screenshot to guide you:

![image](https://user-images.githubusercontent.com/3170758/187794835-60ae3b25-bf94-46b6-a632-a76e60d180eb.png)

Feel free to create as many EBS volumes as you want to track that all of them get appropriately deleted.

As soon as the instance is running, proceed to terminate it. Accept any prompt message from AWS that there are volumes that will be kept in your account.

After a minute, go to CloudWatch dashboard and look for the log group associated to the Lambda function, check the logs where it displays the amount of volumes will be deleted after the lookup. A screenshot is attached:

![Screen Shot 2022-08-31 at 15 14 05](https://user-images.githubusercontent.com/3170758/187795158-a8a5888c-9aa4-49c3-b57e-c0d25aa7c738.png)

If you see this message, that means Lambda was able to delete the volumes found in the execution.

### Scenario #2

You are not tied to create an EC2 instance to see if the Lambda function works or not. You can go directly to the EBS section and create as many volumes as you consider necessary. Since you are not going to attach these volumes to an existing instance, you can see that the Lambda function will proceed to delete them.

Check the logs in CloudWatch to track the progress of the execution.

