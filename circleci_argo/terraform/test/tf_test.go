package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/ec2"
    "github.com/aws/aws-sdk-go/service/eks"
    "github.com/aws/aws-sdk-go/service/iam"
)

func TestTerraformExample(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        TerraformDir: "..",
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    sess, err := session.NewSession(&aws.Config{
        Region: aws.String("eu-north-1")},
    )
    assert.NoError(t, err)

    vpcID := terraform.Output(t, terraformOptions, "vpc_id")
    ec2Client := ec2.New(sess)
    vpc, err := ec2Client.DescribeVpcs(&ec2.DescribeVpcsInput{
        VpcIds: aws.StringSlice([]string{vpcID}),
    })
    assert.NoError(t, err)
    assert.Equal(t, 1, len(vpc.Vpcs))
    assert.Equal(t, "10.0.0.0/16", *vpc.Vpcs[0].CidrBlock)

    subnetIDs := []string{
        terraform.Output(t, terraformOptions, "subnet_1_id"),
        terraform.Output(t, terraformOptions, "subnet_2_id"),
    }
    subnets, err := ec2Client.DescribeSubnets(&ec2.DescribeSubnetsInput{
        SubnetIds: aws.StringSlice(subnetIDs),
    })
    assert.NoError(t, err)
    assert.Equal(t, 2, len(subnets.Subnets))
    assert.ElementsMatch(t, []string{"10.0.1.0/24", "10.0.2.0/24"}, []string{
        *subnets.Subnets[0].CidrBlock,
        *subnets.Subnets[1].CidrBlock,
    })

    igwID := terraform.Output(t, terraformOptions, "igw_id")
    igws, err := ec2Client.DescribeInternetGateways(&ec2.DescribeInternetGatewaysInput{
        InternetGatewayIds: aws.StringSlice([]string{igwID}),
    })
    assert.NoError(t, err)
    assert.Equal(t, 1, len(igws.InternetGateways))
    assert.Equal(t, vpcID, *igws.InternetGateways[0].Attachments[0].VpcId)

    eksClusterName := terraform.Output(t, terraformOptions, "eks_cluster_name")
    eksClient := eks.New(sess)
    cluster, err := eksClient.DescribeCluster(&eks.DescribeClusterInput{
        Name: aws.String(eksClusterName),
    })
    assert.NoError(t, err)
    assert.Equal(t, eksClusterName, *cluster.Cluster.Name)

    masterRoleName := terraform.Output(t, terraformOptions, "master_iam_role_name")
    iamClient := iam.New(sess)
    role, err := iamClient.GetRole(&iam.GetRoleInput{
        RoleName: aws.String(masterRoleName),
    })
    assert.NoError(t, err)
    assert.Equal(t, masterRoleName, *role.Role.RoleName)

    workerRoleName := terraform.Output(t, terraformOptions, "worker_iam_role_name")
    iamClient = iam.New(sess) // Declare iamClient inside the loop
    role, err = iamClient.GetRole(&iam.GetRoleInput{
        RoleName: aws.String(workerRoleName),
    })
    assert.NoError(t, err)
    assert.Equal(t, workerRoleName, *role.Role.RoleName)
}