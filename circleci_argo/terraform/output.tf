output "vpc_id" {
  value = aws_vpc.myvpc.id
  description = "VPC ID of the created VPC"
}

output "subnet_1_id" {
  value = aws_subnet.Mysubnet01.id
  description = "ID of the first public subnet"
}

output "subnet_2_id" {
  value = aws_subnet.Mysubnet02.id
  description = "ID of the second public subnet"
}

output "igw_id" {
  value = aws_internet_gateway.myigw.id
  description = "ID of the internet gateway"
}

output "eks_cluster_name" {
  value = aws_eks_cluster.eks.name
  description = "Name of the EKS cluster"
}

output "iam_master_role_arn" {
  value = aws_iam_role.master.arn
  description = "ARN of the IAM role for EKS cluster master"
}

output "iam_worker_role_arn" {
  value = aws_iam_role.worker.arn
  description = "ARN of the IAM role for EKS worker nodes"
}

output "master_iam_role_name" {
  value = aws_iam_role.master.name
  description = "Name of the IAM role for EKS cluster master"
}

output "worker_iam_role_name" {
  value = aws_iam_role.worker.name
  description = "Name of the IAM role for EKS worker nodes"
}