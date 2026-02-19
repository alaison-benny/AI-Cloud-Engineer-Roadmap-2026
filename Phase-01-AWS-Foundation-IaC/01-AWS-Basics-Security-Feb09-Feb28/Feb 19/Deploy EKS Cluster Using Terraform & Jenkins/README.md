cat << 'EOF' > README.md
# Automated AWS EKS Setup using Jenkins & Terraform 🚀

Jenkins പൈപ്‌ലൈൻ വഴി Terraform ഉപയോഗിച്ച് AWS-ൽ ഒരു Elastic Kubernetes Service (EKS) ക്ലസ്റ്റർ എങ്ങനെ ഓട്ടോമേറ്റഡ് രീതിയിൽ നിർമ്മിക്കാം എന്നതിനെക്കുറിച്ചുള്ള പഠനക്കുറിപ്പുകൾ.

---

## 📂 Overview

താഴെ പറയുന്ന stepsലൂടെയാണ് ഒരു കുബെർനെറ്റീസ് ക്ലസ്റ്റർ സജ്ജീകരിക്കുന്നത്:

1. **Jenkins Server Setup**: ഒരു AWS EC2 ഇൻസ്റ്റൻസിൽ Jenkins, Terraform, AWS CLI, Kubectl എന്നിവ ഇൻസ്റ്റാൾ ചെയ്യുന്നു [00:03:06].
2. **Infrastructure as Code (IaC)**: Terraform ഉപയോഗിച്ച് VPC-യും EKS ക്ലസ്റ്ററും നിർമ്മിക്കാനുള്ള കോഡ് തയ്യാറാക്കുന്നു.
3. **Jenkins CI/CD Pipeline**: GitHub-ൽ നിന്ന് കോഡ് എടുത്ത് ഓട്ടോമാറ്റിക്കായി AWS-ൽ ക്ലസ്റ്റർ നിർമ്മിക്കുന്ന പൈപ്‌ലൈൻ സെറ്റ് ചെയ്യുന്നു.
4. **Validation**: നിർമ്മിച്ച ക്ലസ്റ്ററിൽ ഒരു Nginx Pod റൺ ചെയ്ത് പ്രവർത്തനം ഉറപ്പുവരുത്തുന്നു [00:42:11].

---

## 🏗️ പ്രധാന ടൂളുകളും കമാൻഡുകളും (Tools & Commands)

ഈ പ്രോജക്റ്റിൽ ഉപയോഗിച്ചിരിക്കുന്ന ഓരോ കമാൻഡും എന്തിനാണെന്ന് താഴെ വിശദീകരിക്കുന്നു:

### 1. Terraform കമാൻഡുകൾ
* `terraform init`: ടെറാഫോം വർക്കിംഗ് ഡയറക്ടറി ഇനീഷ്യലൈസ് ചെയ്യാനും ആവശ്യമായ പ്രൊവൈഡർ പ്ലഗിന്നുകൾ ഡൗൺലോഡ് ചെയ്യാനും [00:31:17].
* `terraform plan`: നിർമ്മിക്കപ്പെടാൻ പോകുന്ന റിസോഴ്സുകൾ (VPC, EKS) ഏതൊക്കെയെന്ന് മുൻകൂട്ടി പരിശോധിക്കാൻ [00:32:40].
* `terraform apply`: AWS-ൽ യഥാർത്ഥ റിസോഴ്സുകൾ നിർമ്മിക്കാൻ [00:33:03].
* `terraform destroy`: പഠനം കഴിഞ്ഞാൽ എല്ലാ റിസോഴ്സുകളും ഒറ്റയടിക്ക് ഡിലീറ്റ് ചെയ്യാൻ [00:43:22].

### 2. Kubernetes കമാൻഡുകൾ (kubectl)
* `aws eks update-kubeconfig --region <region> --name <cluster-name>`: നിങ്ങളുടെ ലോക്കൽ കമ്പ്യൂട്ടറിലോ Jenkins സെർവറിലോ ഉള്ള `kubectl`-നെ പുതിയ EKS ക്ലസ്റ്ററുമായി കണക്ട് ചെയ്യാൻ [00:41:40].
* `kubectl get pods`: ക്ലസ്റ്ററിൽ റൺ ചെയ്യുന്ന ആപ്ലിക്കേഷനുകളുടെ (Pods) വിവരങ്ങൾ അറിയാൻ [00:42:11].
* `kubectl run nginx --image=nginx`: ടെസ്റ്റിംഗിനായി ഒരു Nginx പോഡ് ക്രിയേറ്റ് ചെയ്യാൻ [00:42:27].

---

## 📝 പൈപ്‌ലൈൻ ഘട്ടങ്ങൾ (Pipeline Stages)

Jenkinsfile-ൽ ഉൾപ്പെടുത്തിയിരിക്കുന്ന പ്രധാന സ്റ്റേജുകൾ ഇവയാണ്:

1. **Checkout**: GitHub-ൽ നിന്ന് കോഡ് ഡൗൺലോഡ് ചെയ്യുന്നു.
2. **Terraform Init & Validate**: കോഡിലെ തെറ്റുകൾ പരിശോധിക്കുന്നു.
3. **Terraform Plan**: മാറ്റങ്ങൾ കാണിച്ചുതരുന്നു.
4. **Approval**: ഉപയോക്താവ് 'Proceed' നൽകുന്നത് വരെ കാത്തിരിക്കുന്നു (സുരക്ഷയ്ക്കായി).
5. **Terraform Apply/Destroy**: തിരഞ്ഞെടുത്ത ഓപ്ഷൻ അനുസരിച്ച് ക്ലസ്റ്റർ നിർമ്മിക്കുകയോ ഒഴിവാക്കുകയോ ചെയ്യുന്നു.

---

## 🛠️ ഭാവിയിലേക്കുള്ള ചില നിർദ്ദേശങ്ങൾ (Future Purposes)

* **IAM Permissions**: Jenkins സെർവറിന് AWS-ൽ റിസോഴ്സുകൾ നിർമ്മിക്കാൻ ആവശ്യമായ അനുമതികൾ (IAM Roles) നൽകാൻ ശ്രദ്ധിക്കുക.
* **Credentials**: AWS Access Key, Secret Key എന്നിവ Jenkins-ൽ `secret text` ആയി വേണം സൂക്ഷിക്കാൻ.
* **Cost Management**: പഠനം കഴിഞ്ഞാലുടൻ `terraform destroy` ഉപയോഗിച്ച് ക്ലസ്റ്റർ നീക്കം ചെയ്യുക, കാരണം EKS ഉപയോഗിക്കുന്നതിന് മണിക്കൂർ അടിസ്ഥാനത്തിൽ ചാർജ് ഈടാക്കുന്നതാണ്.

---
*ഈ വീഡിയോ കാണുക: [Deploy EKS Cluster Using Terraform & Jenkins](https://youtu.be/byxQr7RaaoM)*
EOF
