from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status, permissions, generics
from .models import Comment, Reply
from users.models import User
from resources.models import Resources
from .serializers import CommentSerializer, ReplySerializer
# Create your views here.
####Comment by U Resource ID
class CommentView(generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk):
        try:
            resource = Resources.objects.get(id=pk)
            if resource:
                comments = Comment.objects.filter(resource=resource)
                if comments:
                    ser = CommentSerializer(comments, many=True)
                    return JsonResponse({"comments":ser.data})
                else:
                    return JsonResponse({"error":"Comments Doesnot Exist"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({"error":"Resource Doesnot found"}, status=status.HTTP_404_NOT_FOUND)
        except Execption:
            return JsonResponse({"ServerError":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, pk):
        comment = request.data.get("comment")
        ###user_id == request.user.id
        user_id = request.data.get("user_id")
        if comment:
            resource = Resources.objects.get(id=pk)
            user = User.objects.get(id=user_id)
            if resource and user:
                comment = Comment(comment=comment, resource=resource, user=user)
                comment.save()
                ser = CommentSerializer(comment)
                return JsonResponse({"comment Created":ser.data})
            return JsonResponse({"error":"resource or user doesnot exist"})
        else:
            return JsonResponse({"error":"Cant create an empty comment"})
class CommentDetail(generics.GenericAPIView):
    queryset = [Comment.objects.all(), Reply.objects.all()]
    serializer_class = [CommentSerializer, ReplySerializer]
    permission_classes = [permissions.AllowAny]

    ####Post Reply
    def post(self, request, pk):
        reply = request.data.get("comment")
        user_id = request.data.get("user_id")
        if reply and user_id:
            user = User.objects.get(id=user_id)
            comment = Comment.objects.get(id=pk)
            if comment and user:
                reply = Reply(reply=reply, comment=comment, user=user)
                reply.save()
                ser = ReplySerializer(reply)
                return JsonResponse({"Reply Created":ser.data})
            return JsonResponse({"error":"User or Comment Doesnot Found"})
        else:
            return JsonResponse({"error":"Cant create an empty reply"})
    def put(self, request, pk):
        comment = Comment.objects.get(id=pk)
        if comment:
            comment2 = request.data.get("comment")
            if comment2:
                comment.comment = comment2
                comment.save()
                ser = CommentSerializer(comment)
                return JsonResponse({"error":"comment Updated Succesfully", "comment":ser.data}, status.HTTP_201_CREATED)
            else:
                return JsonResponse({"error":"Please enter some message"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"error":"Comment doesnot Found"}, status=status.HTTP_404_NOT_FOUND)
    #### Fetch REplies and detail Comment
    def get(self, request, pk):
        comment = Comment.objects.get(id=pk)
        if comment:
            reply = Reply.objects.filter(comment=comment)
            # ser_comment = CommentSerializer(comment)
            ser_reply = ReplySerializer(reply, many=True)

            return JsonResponse({"reply":ser_reply.data}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error":"Comment doesnot Found"}, status=status.HTTP_400_BAD_REQUEST)