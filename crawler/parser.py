from crawler import Crawler
import datetime as dt
import xlwt
from xlwt import Workbook

sentimentIdx = 0
titleIdx = 1
urlIdx = 2
dateIdx = 3
upvoteIdx = 4
downvoteIdx = 5
commentsIdx = 7

numOfComments = 10

def parse_reddit(submissions):
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')

    sheet1.write(0, sentimentIdx, "SENTIMENT")
    sheet1.write(0, titleIdx, "TITLE")
    sheet1.write(0, urlIdx, "URL")
    sheet1.write(0, dateIdx, "DATE")
    sheet1.write(0, upvoteIdx, "UPVOTE")
    sheet1.write(0, downvoteIdx, "DOWNVOTE")
    sheet1.write(0, commentsIdx, "COMMENTS")

    for rowNum in range(len(submissions)):
        print("Grabbing submissions " + str(rowNum))
        sheet1.write(rowNum + 1, titleIdx, submissions[rowNum].title)
        sheet1.write(rowNum + 1, urlIdx, submissions[rowNum].url)
        sheet1.write(rowNum + 1, dateIdx, submissions[rowNum].created)
        sheet1.write(rowNum + 1, upvoteIdx, submissions[rowNum].score)
        sheet1.write(rowNum + 1, downvoteIdx, submissions[rowNum].score / submissions[rowNum].upvote_ratio - submissions[rowNum].score)
        comments = crawler.get_comments(submissions[rowNum], numOfComments)  # grabbing top 10 texts
        commentBlock = ""
        for comment in comments:
            commentBlock = commentBlock + comment.body + "\n"
        sheet1.write(rowNum + 1, commentsIdx, commentBlock)

    wb.save('redditCrawlerData.xls')

if __name__ == "__main__":
    start = dt.datetime(2017, 1, 1)
    end = dt.datetime(2018, 1, 1)

    crawler = Crawler()
    submissions = crawler.crawl("worldnews", start, end, 100) #grabbing 100 submissions from 2017/1/1 to 2018/1/1
    parse_reddit(submissions)



