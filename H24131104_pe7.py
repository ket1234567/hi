def analyze_forum(file_paths):
    # 定義處理每個留言的遞迴函數
    def process_comment(post_id, comment_id, comment_data, depth, total_likes, author_likes, flattened):
        # 記錄展平的結果
        flattened.append((post_id, comment_id, depth, comment_data['likes']))
        # 累加 post 的 total_likes
        total_likes[post_id] += comment_data['likes']
        # 累加作者的 likes
        author = comment_data['author']
        author_likes[author] = author_likes.get(author, 0) + comment_data['likes']
        # 處理巢狀回覆
        for reply_id, reply_data in sorted(comment_data['replies'].items()):
            process_comment(post_id, reply_id, reply_data, depth + 1, total_likes, author_likes, flattened)
    
    # 遍歷每個論壇檔案
    for file_path in file_paths:
        
        print(f"\n=== Result for {file_path} ===\n")
        total_likes = {}
        author_likes = {}
        flattened = []
        
        with open(file_path, 'r') as file:
            # 讀取數據，移除 'forum =' 前綴
            data_str = file.read().strip()
            data_str = data_str[data_str.index('=') + 1:].strip()
            # 轉換為字典
            data = eval(data_str)
            
            # 遍歷每個帖子
            for post_id, post_data in sorted(data.items()):
                # 初始化這個 post 的 total_likes
                total_likes[post_id] = 0
                # 處理每個 comment
                for comment_id, comment_data in sorted(post_data['comments'].items()):
                    process_comment(post_id, comment_id, comment_data, 1, total_likes, author_likes, flattened)
        
        # 找出 total_likes 中最大按讚數的 post_id
        max_likes_post = max(total_likes, key=total_likes.get)
        
        # 建立最終結果字典
        result = {
            'total_likes': total_likes,
            'max_likes_post': max_likes_post,
            'flattened': flattened,
            'author_likes': dict(sorted(author_likes.items()))
        }
        
        # 格式化輸出
        print('total_likes:')
        for k, v in result['total_likes'].items():
            print(f'    {k}: {v}')
        print('\nmax_likes_post:')
        print(f'    {result["max_likes_post"]}')
        print('\nflattened:')
        for item in result['flattened']:
            print(f'    {item},')
        print('\nauthor_likes:')
        for k, v in result['author_likes'].items():
            print(f'    {k}: {v},')

analyze_forum(['forum1.txt', 'forum2.txt'])
