import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


df = pd.read_csv("Details_of_Har_Ghar_Jal.csv")

total_panchayat = df["No. of panchayats"].sum()
total_villages = df["No. of villages"].sum()
reported_panchayat = df["No. of Har Ghar Jal Panchayat-Reported"].sum()
certified_village = df["No. of Har Ghar Jal Village-Certified"].sum()
No_of_block= df["No. of block"].sum()

print(".....Total Coverage Indicators.....")
print("Total District:",df["District Name"].count())
print("Total Panchayats:", total_panchayat)
print("Total Villages:", total_villages)
print("Reported Panchayats:", reported_panchayat)
print("Certified Villages:", certified_village)
print("No of block :", No_of_block)

print(".....Block cert rate.....")
df["Block_Cert_%"] = (
        df["No. of Har Ghar Jal Block-Certified"] /
        df["No. of block"]
) * 100
print(df["Block_Cert_%"])


print(".....Panchayat coverage rate.....")
df["Panchayat_coverage_%"] = (
               df["No. of Har Ghar Jal Panchayat-Reported"]/
               df["No. of panchayats"]
               ) * 100
print(df["Panchayat_coverage_%"])


print(".....Village certification rate.....")
df["Village_certification_%"] = (
        df["No. of Har Ghar Jal Village-Certified"]/
        df["No. of villages"]
         ) * 100
print(df["Village_certification_%"])


print(".....Create performance score.....")
df["Create_performance_score"] = (
        df["Block_Cert_%"]+df["Panchayat_coverage_%"]+df["Village_certification_%"]
                 )/3
print(df["Create_performance_score"])


print(".....Rank districts.....")
ranking = df.sort_values(by=["Create_performance_score"], ascending=False)
print(ranking[["District Name","Create_performance_score"]].head(5))
print(ranking[["District Name","Create_performance_score"]].tail(5))


print(".....Calculate gap.....")
print("1. Village_Gap")
df["Village_Gap"] = (
        df["No. of villages"] -
        df["No. of Har Ghar Jal Village-Certified"]
                    )
gap = df.sort_values("Village_Gap", ascending=False)
print(gap[["District Name","Village_Gap"]].head(5))
print(gap[["District Name","Village_Gap"]].tail(5))

print("1. Large gap → many villages still without certification.\n2. Policy makers focus on these districts.")

print("2. Panchayat_Gap")
df["Panchayat_Gap"] = (
    df["No. of panchayats"] -
    df["No. of Har Ghar Jal Panchayat-Reported"]
                     )
gap = df.sort_values("Panchayat_Gap", ascending=False)
print(gap[["District Name","Panchayat_Gap"]].head(5))
print(gap[["District Name","Panchayat_Gap"]].tail(5))

print("1. Large gap → many Panchayat still without certification.\n2. Policy makers focus on these districts.")

print("3. Block_Gap")
df["Block_Gap"] = (
    df["No. of block"] -
    df["No. of Har Ghar Jal Block-Certified"]
                )
gap = df.sort_values("Block_Gap", ascending=False)
print(gap[["District Name","Block_Gap"]].head(5))
print(gap[["District Name","Block_Gap"]].tail(5))

print("1. Large gap → many Panchayat still without certification.\n2. Policy makers focus on these districts.")


# Visualization
top10 = df.sort_values("Create_performance_score", ascending=False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(x="Create_performance_score", y="District Name", data=top10)
plt.title("Top 10 Districts by 'Har Ghar Jal Performance Score'")
plt.xlabel("Performance Score")
plt.ylabel("District")
plt.savefig("Top 10 Districts by 'Har Ghar Jal Performance Score'.png")
plt.show()

bottom10 = df.sort_values("Create_performance_score", ascending=True).head(10)
plt.figure(figsize=(10,5))
sns.barplot(x="Create_performance_score", y="District Name", data=bottom10)
plt.title("Bottom 10 Districts by 'Har Ghar Jal Performance Score'")
plt.xlabel("Performance Score")
plt.ylabel("District")
plt.savefig("Bottom 10 Districts by 'Har Ghar Jal Performance Score'.png")
plt.show()

top10_gap = df.sort_values("Village_Gap", ascending=False).head(10)
plt.figure(figsize=(10,5))
sns.barplot(x="Village_Gap", y="District Name", data=top10_gap)
plt.title("Top 10 Districts by Village Certification Gap")
plt.xlabel("Village Gap")
plt.ylabel("District")
plt.savefig("Top 10 Districts by Village Certification Gap.png")
plt.show()


print(".....Implementation Efficiency.....")
df["Implementation_Efficiency"] = (
    df["No. of Har Ghar Jal Village-Certified"]/df["No. of Har Ghar Jal Village-Reported"]
) * 100
print(df["Implementation_Efficiency"])

ineff10 = df.sort_values("Implementation_Efficiency", ascending=False).head(10)
print(ineff10[["District Name","Implementation_Efficiency"]])
plt.figure(figsize=(10,5))
sns.barplot(x="Create_performance_score", y="District Name", data=ineff10),
plt.title("Top 10 Districts by 'Implementation_Efficiency'")
plt.xlabel("Implementation_Efficiency")
plt.ylabel("District")
plt.savefig("Top 10 Districts by 'Implementation_Efficiency'.png")
plt.show()


print(".....Correlation Analysis.....")
corr = df.corr(numeric_only=True)
plt.figure(figsize=(15,15))
sns.heatmap(corr,annot=True,cmap="coolwarm")
plt.title("Correlation Heatmap of Har Ghar Jal Indicators")
plt.savefig("Correlation Heatmap of Har Ghar Jal Indicators.png")
plt.show()


print(".....Distribution of Village Certification Rate.....")
plt.figure(figsize=(8,5))
sns.histplot(df["Village_certification_%"],bins=10,kde=True)
plt.title("Distribution of Village Certification Percentage")
plt.xlabel("Village Certification (%)")
plt.ylabel("Number of Districts")
plt.savefig("Distribution of Village Certification Percentage.png")
plt.show()


print(".....Village Certification Statistics.....")
print(df["Village_certification_%"].describe())

avg_cert = df["Village_certification_%"].mean()
print("Average Village Certification Rate:", round(avg_cert,2), "%")

best = df.loc[df["Village_certification_%"].idxmax()]
print("Best District:")
print(best[["District Name","Village_certification_%"]])

worst = df.loc[df["Village_certification_%"].idxmin()]
print("Worst District:")
print(worst[["District Name","Village_certification_%"]])

below_avg = df[df["Village_certification_%"] < avg_cert]
print("Districts Below Average Performance:")
print(below_avg[["District Name","Village_certification_%"]])

df.to_csv("har_ghar_jal_processed_data.csv", index=False)
print("Processed dataset saved successfully")

